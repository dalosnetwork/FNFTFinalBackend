// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "../interface/IERC721.sol";

contract Vault {
    address erc721Address;
    address owner;

    mapping(address => bool) cleanList;
    mapping(uint256 => address) NFTreferToken;
    mapping(address => uint256) TokenreferNFT;

    modifier onlyClean() {
        require(cleanList[msg.sender], "Not in clean list");
        _;
    }

    modifier onlyOwner() {
        require(owner == msg.sender);
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function deposit(uint256 _tokenID, address _owner) public onlyClean() returns(bool) {
        require(NFTreferToken[_tokenID] == address(0), "NFT already deposited"); // NFT not already deposited
        
        IERC721 _erc721 = IERC721(erc721Address);

        require(_erc721.ownerOf(_tokenID) == _owner, "NFT not owned by user"); // NFT ownership
        require(_erc721.isApprovedForAll(_owner, address(this)), "NFT not approved for transfer"); // Approved for transfer

        _erc721.transferFrom(_owner, address(this), _tokenID); // NFT transfer to vault

        return true;
    }

    function redeemAll(uint256 _tokenID, address _owner) public onlyClean() returns(bool) {
        require(NFTreferToken[_tokenID] != address(0), "NFT not deposited"); // NFT already deposited

        IERC721 _erc721 = IERC721(erc721Address);

        require(_erc721.ownerOf(_tokenID) == address(this), "NFT not owned by vault"); // NFT ownership

        _erc721.transferFrom(address(this), _owner, _tokenID); // NFT transfer to user

        address _erc20Address = NFTreferToken[_tokenID]; // Get ERC20 address
        NFTreferToken[_tokenID] = address(0x0); // Delete NFT reference
        TokenreferNFT[_erc20Address] = 0; // Delete token reference

        return true;
    }

    function getTokenreferNFT(address _erc20Address) public view returns (uint256) {
        return TokenreferNFT[_erc20Address];
    }

    function addTokenreferNFT(address _erc20Address, uint256 _tokenID) public onlyClean() {
        TokenreferNFT[_erc20Address] = _tokenID;
    }

    function getNFTreferToken(uint256 _tokenID) public view returns (address) {
        return NFTreferToken[_tokenID];
    }

    function addNFTreferToken(uint256 _tokenID, address _erc20Address) public onlyClean() {
        NFTreferToken[_tokenID] = _erc20Address;
    }

    function addToCleanList(address _cleanAddress) public onlyOwner() {
        cleanList[_cleanAddress] = true;
    }

    function removeFromCleanList(address _cleanAddress) public onlyClean() {
        cleanList[_cleanAddress] = false;
    }

    function getErc721Address() public view returns (address) {
        return erc721Address;
    }

    function setErc721Address(address newErc721Address) public onlyClean() {
        erc721Address = newErc721Address;
    }
}