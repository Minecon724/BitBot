package pl.minecon724.bitbot.utils;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import pl.minecon724.bitbot.BitBot;

public class EcoManager {
	BitBot bitbot;
	public EcoManager(BitBot bitbot) throws SQLException, ClassNotFoundException {
		this.bitbot = bitbot;
		Class.forName("com.mysql.jdbc.Driver");
		Connection con = DriverManager.getConnection(bitbot.args[1], bitbot.args[2], bitbot.args[3]);
		System.out.println("Connected to " + bitbot.args[1]);
	}
	
}
