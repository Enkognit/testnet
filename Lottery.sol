pragma solidity ^0.8.24;

contract Lottery {
    mapping(address => uint256) private balances;
    
    address[] public keys;

    uint256 public endLotteryTime;

    uint256 public lotteryTime;

    address private owner;

    event BoughtTicket(
        address buyer,
        uint256 price
    );

    constructor() {
        owner = msg.sender;
        lotteryTime = 60;
        endLotteryTime = block.timestamp + lotteryTime;
    }

    function currentPrize() public view returns (uint256) {
        return address(this).balance;
    }

    function buyLotteryTicket() public payable {
        require(msg.value > 0);
        require(block.timestamp <= endLotteryTime, "Lottery is not commited");
        if (balances[msg.sender] == 0) {
            keys.push(msg.sender);
        }
        balances[msg.sender] += msg.value;
        emit BoughtTicket(msg.sender, msg.value);
    }

    event EndLottery(
        address winner,
        uint256 prize
    );

    function endLottery() public {
        require(msg.sender == owner || block.timestamp > endLotteryTime, "Lottery is not finished");

        uint256 balance = address(this).balance;

        if (balance < 1000000) { 
            return;
        }

        uint256 prize = balance - balance / 1000;

        uint256 randomNumber = getRandom(address(this).balance);
        uint256 cur = 0;
        address payable winner;
        for (uint256 i = 0; i < keys.length; i++) {
            cur = cur + balances[keys[i]];
            delete balances[keys[i]];
            if (cur >= randomNumber) {
                winner = payable(keys[i]);
                break;
            }
        }

        winner.transfer(prize);
        payable(msg.sender).transfer(balance - prize);

        delete keys;

        endLotteryTime = block.timestamp + lotteryTime; 
        emit EndLottery(winner, prize);
    }

    function changeLotteryTime(uint256 newLotteryTime) public isOwner {
        require(newLotteryTime > 5, "New time is too small");
        lotteryTime = newLotteryTime;
    }

    modifier isOwner() {
        require(msg.sender == owner, "Must be owner to create");
        _;
    }

    function getRandom(uint256 n) private returns (uint256) {
        require(n > 0, "n must be positive");
        uint256 randomNumber = uint256(keccak256(abi.encodePacked(
            block.timestamp, 
            block.difficulty,
            block.number,
            address(this).balance
        )));
        return (randomNumber % (n + 1)) + 1;
    }
}