package pl.minecon724.bitbot.utils;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;


public class EcoManager {
	public EcoManager(String dbUrl) throws SQLException, ClassNotFoundException {
		Class.forName("com.mysql.jdbc.Driver");
		Connection con = DriverManager.getConnection(dbUrl);
		System.out.println("Connected to database");
	}
	
}
