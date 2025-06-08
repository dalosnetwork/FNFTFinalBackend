// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract CertNFT is ERC721URIStorage {
    uint256 private _nextTokenId = 1;
    address owner;

    constructor() ERC721("CertNFT", "CNFT") {
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
