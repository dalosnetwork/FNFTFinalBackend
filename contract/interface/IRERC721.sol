// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

interface IRERC721 {
    function mint(address to, string calldata metadataURI) external;
    function ownerOf(uint256 tokenId) external view returns (address);
    function transferFrom(address from, address to, uint256 tokenId) external;
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}
