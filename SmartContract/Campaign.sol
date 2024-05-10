pragma solidity ^0.4.17;

contract Campaign {
    struct Request {
        string description;
        uint value;
        address recipient;
        bool complete;
        uint approvalCount;
        mapping (address => bool) approvals;
    }

    Request[] public requests;
    address public manager;
    uint public minimumContribution;
    mapping (address => bool) public approvers; // address is not stored in mapping!
    uint public approversCount = 0;

    modifier restricted() {
        require(msg.sender == manager);
        _;
    }

    function Campaign(uint minimum, address creater) public  {
        manager = creater;
        minimumContribution = minimum;
    }

    function contribute() public  payable {
        require(msg.value > minimumContribution);
        approvers[msg.sender] = true;
        approversCount++;
    }

    function createRequest(string _description, uint _value, address _reipient) public restricted payable {
        Request memory newRequest = Request({
            description:_description,
            value:_value,
            recipient:_reipient,
            complete: false,
            approvalCount : 0
        });

        requests.push(newRequest);
    }

    function approveRequest(uint index) public payable {
        Request storage request = requests[index];

        require(approvers[msg.sender]); //he should donater
        require(index < requests.length);
        require(!request.approvals[msg.sender]); // only one time vote allowed
        request.approvals[msg.sender] = true;
        request.approvalCount++;
    }

    function finalizeRequest(uint index) public restricted payable {
        Request storage request = requests[index];

        require(!request.complete);
        require(request.approvalCount > (approversCount / 2));
        request.complete = true;
        request.recipient.transfer(request.value);
    }

    function getSummary() public view returns (uint,uint,uint,uint,address) {
        return (
            minimumContribution,
            this.balance,
            requests.length,
            approversCount,
            manager
        );
    }

    function getRequestsCount() public view returns (uint) {
        return requests.length;
    }
}