package pl.minecon724.bitbot.utils;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import pl.minecon724.bitbot.commands.MarketCommand;
import pl.minecon724.bitbot.exceptions.InsufficientBalance;


public class EcoManager {
	MarketCommand marketCmd;
	
	public EcoManager(String dbUrl) throws SQLException, ClassNotFoundException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection con = DriverManager.getConnection(dbUrl);
		System.out.println("Connected to database");
	}
	
	public double getBalance(int uid, String asset) {
		// TODO
		return 0;
	}
	
	public void setBalance(int uid, String asset, double amount) {
		// TODO
		return;
	}
	
	public double convertPrice(String from, String to, double quantity) {
		// TODO
		return 0;
	}
	
	public double exchange(int uid, String from, String to, double quantity) throws InsufficientBalance {
		double currentBalance = getBalance(uid, from);
		if (quantity > currentBalance) {
			throw new InsufficientBalance("You don't have " + quantity + " " + from);
		}
		double price = convertPrice(from, to, quantity);
		setBalance(uid, from, currentBalance - quantity);
		setBalance(uid, to, getBalance(uid, to) + price);
		return price;
	}
	
}
