// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

interface IVault {
        function deposit(uint256 _tokenID, address _owner) external returns (bool);
        function redeemAll(uint256 _tokenID, address _owner) external returns (bool);
        function getTokenreferNFT(address _erc20Address) external view returns (uint256);
        function addTokenreferNFT(address _erc20Address, uint256 _tokenID) external;
        function addNFTreferToken(uint256 _tokenID, address _erc20Address) external;
}