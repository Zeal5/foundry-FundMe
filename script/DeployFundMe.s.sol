// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.23;

import {Script,console} from "forge-std/Script.sol";
import {FundMe} from "../src/FundMe.sol";



contract DeployFundMe is Script {
	function run() external returns (FundMe) {
		vm.startBroadcast();
		// address here
		FundMe fundme = new FundMe();
		return fundme;
	}

}

