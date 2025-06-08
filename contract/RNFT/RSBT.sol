// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract RSBT is ERC721URIStorage {
    uint256 private _nextTokenId = 1;
    address owner;

    constructor() ERC721("RSBT", "RSBT") {
        owner = msg.sender;
    }

    function mint(address to, string memory metadataURI) external {
        require(to == owner);

        uint256 tokenId = _nextTokenId;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, metadataURI);
        _nextTokenId++;
    }

    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory data) public pure override(ERC721, IERC721) {
        revert("SBT: transfer not allowed");
    }

    function approve(address to, uint256 tokenId) public override(ERC721, IERC721) {
        revert("SBT: approval not allowed");
    }

    function setApprovalForAll(address operator, bool approved) public pure override(ERC721, IERC721) {
        revert("SBT: setApprovalForAll not allowed");
    }
}
