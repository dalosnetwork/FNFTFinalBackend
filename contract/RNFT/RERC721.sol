// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract RERC721 is ERC721URIStorage {
    uint256 private _nextTokenId = 1;
    address owner;

    constructor() ERC721("RERC721", "RERC721") {
        owner = msg.sender;
    }

    function mint(address to, string memory metadataURI) external {
        require(owner == to);

        uint256 tokenId = _nextTokenId;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, metadataURI);
        _nextTokenId++;
    }
}
