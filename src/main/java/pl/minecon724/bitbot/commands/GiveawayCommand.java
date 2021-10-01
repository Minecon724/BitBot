package pl.minecon724.bitbot.commands;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

import pl.minecon724.bitbot.utils.Giveaway;

public class GiveawayCommand {
	String dbUrl;
	Connection con;
	List<Giveaway> queue;
	public GiveawayCommand(String dbUrl) throws ClassNotFoundException, SQLException {
		Class.forName("com.mysql.jdbc.Driver");
		con = DriverManager.getConnection(dbUrl);
		System.out.println("[Giveaway] Connected to database");
	}
	
	public void end(Giveaway gw) {
		// TODO
		return;
	}
	
	public void start(Giveaway gw) {
		// TODO
		return;
	}
	
	public void reroll(Giveaway gw) {
		// TODO
		return;
	}
	
	public void setupDatabase(Connection con, boolean reset) throws SQLException {
		Statement stt;
		if (reset) {
			stt = con.createStatement();
			stt.execute("drop table giveaways");
			stt.close();
		}
		stt = con.createStatement();
		stt.execute("create table giveaways (message int not null, prize text not null, ending int not null, winners int not null, ended tinyint(1) not null");
		stt.close();
	}
	
	public class refresh implements Runnable {
		@Override
		public void run() {
			Statement stt;
			ResultSet rs;
			try {
				stt = con.createStatement();
				stt.execute("select * from giveaways");
				rs = stt.getResultSet();
				long time = System.currentTimeMillis() / 1000;
				while (rs.next()) {
					long ending = rs.getLong("ending");
					if (time+60 >= ending) {
						Giveaway gw = new Giveaway(rs.getInt("message"), rs.getString("prize"), ending, rs.getInt("winners"));
						queue.add(gw);
					}
					if (time >= ending) {
						Giveaway gw = new Giveaway(rs.getInt("message"), rs.getString("prize"), ending, rs.getInt("winners"));
						end(gw);
					}
				}
				rs.close();
				stt.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
	}
}
