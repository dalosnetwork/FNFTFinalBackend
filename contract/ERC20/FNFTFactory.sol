// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "./FNFT.sol";

contract FNFTFactory {
    event TokenCreated(address, string, string, uint256, address);
    
    function createToken(string memory _name, string memory _symbol, uint256 _initialSupply, address _owner) external returns (address) {
        FNFT newToken = new FNFT(_name, _symbol, _initialSupply, _owner);

        emit TokenCreated(address(newToken), _name, _symbol, _initialSupply, _owner);

        return address(newToken);
    }
}
