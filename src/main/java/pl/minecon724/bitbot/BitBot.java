package pl.minecon724.bitbot;

import java.sql.SQLException;

import javax.security.auth.login.LoginException;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import pl.minecon724.bitbot.commands.Commands;
import pl.minecon724.bitbot.listeners.EventReady;
import pl.minecon724.bitbot.utils.EcoManager;

public class BitBot {
	static EcoManager ecoMan;
	
	public static void main(String[] args) throws LoginException, ClassNotFoundException, SQLException {
		//ecoMan = new EcoManager(args[1]);
		JDA jda = JDABuilder.createDefault(args[0]).build();
		jda.addEventListener(new EventReady());
		jda.addEventListener(new Commands());
	}
}
