package pl.minecon724.bitbot;

import javax.security.auth.login.LoginException;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;

public class BitBot {
	public void main(String[] args) throws LoginException {
		JDA jda = JDABuilder.createDefault(args[0]).build();
	}
}
