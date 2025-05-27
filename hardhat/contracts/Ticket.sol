// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";


contract Ticket is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    struct TicketData {
        uint256 id;
        string eventName; 
        string date;       
        string zone;       
        string seat;      
        uint256 price;  
    }

    mapping(uint256 => TicketData) public tickets;
    mapping(address => uint256[]) private _userTickets;

    constructor() ERC721("ConcertTicket", "TICKET") {}

    function mintTicket(
        address buyer,
        string memory eventName,
        string memory date,
        string memory zone,
        string memory seat,
        uint256 price
    ) public payable {
        require(msg.value >= price, "Insufficient payment for ticket");

        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _safeMint(buyer, newTokenId);

        tickets[newTokenId] = TicketData({
            id: newTokenId,
            eventName: eventName,
            date: date,
            zone: zone,
            seat: seat,
            price: price
        });

        _userTickets[buyer].push(newTokenId);
    }

    function getUserTickets(address user) public view returns (
        string[] memory eventNames,
        string[] memory dates,
        string[] memory zones,
        string[] memory seats,
        uint256[] memory prices
    ) {
        uint256[] memory userTicketIds = _userTickets[user];
        uint256 length = userTicketIds.length;

        eventNames = new string[](length);
        dates = new string[](length);
        zones = new string[](length);
        seats = new string[](length);
        prices = new uint256[](length);

        for (uint256 i = 0; i < length; i++) {
            TicketData memory ticket = tickets[userTicketIds[i]];
            eventNames[i] = ticket.eventName;
            dates[i] = ticket.date;
            zones[i] = ticket.zone;
            seats[i] = ticket.seat;
            prices[i] = ticket.price;
        }
    }
}