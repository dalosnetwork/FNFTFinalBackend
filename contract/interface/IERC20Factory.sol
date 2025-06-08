// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

interface IERC20Factory {
    function createToken(string memory _name, string memory _symbol, uint256 _initialSupply, address _owner) external returns (address);

}