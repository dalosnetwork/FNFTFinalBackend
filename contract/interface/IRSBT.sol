// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

interface IRSBT {
    function mint(address to, string calldata metadataURI) external;
    function ownerOf(uint256 tokenId) external view returns (address);
}
