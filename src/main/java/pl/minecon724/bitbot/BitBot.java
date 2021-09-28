package pl.minecon724.bitbot;

import java.sql.SQLException;

import javax.security.auth.login.LoginException;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import pl.minecon724.bitbot.commands.Commands;
import pl.minecon724.bitbot.listeners.EventReady;
import pl.minecon724.bitbot.utils.EcoManager;

public class BitBot {
	public String[] args;
	EcoManager ecoMan;
	
	public void main(String[] args) throws LoginException, ClassNotFoundException, SQLException {
		this.args = args;
		ecoMan = new EcoManager(this);
		JDA jda = JDABuilder.createDefault(args[0]).build();
		jda.addEventListener(new EventReady(this));
		jda.addEventListener(new Commands(this));
	}
}
