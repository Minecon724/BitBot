package pl.minecon724.bitbot;

import java.sql.SQLException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import javax.security.auth.login.LoginException;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import pl.minecon724.bitbot.commands.Commands;
import pl.minecon724.bitbot.listeners.EventReady;
import pl.minecon724.bitbot.utils.EcoManager;
import pl.minecon724.bitbot.utils.StatusChange;

public class BitBot {
	static EcoManager ecoMan;
	
	public static void main(String[] args) throws LoginException, ClassNotFoundException, SQLException {
		//ecoMan = new EcoManager(args[1]);
		JDA jda = JDABuilder.createDefault(args[0]).build();
		jda.addEventListener(new EventReady());
		jda.addEventListener(new Commands());
		jda.upsertCommand("help", "Show all commands");
		CommandData exchangeCmd = new CommandData("exchange", "Exchange assets");
		exchangeCmd.addOption(OptionType.STRING, "From", "Asset you want to sell");
		exchangeCmd.addOption(OptionType.STRING, "To", "Asset you want to buy");
		exchangeCmd.addOption(OptionType.INTEGER, "Quantity", "Quantity of the asset you want to SELL");
		jda.upsertCommand(exchangeCmd);
		CommandData marketCmd = new CommandData("market", "View market");
		marketCmd.addOption(OptionType.STRING, "Asset", "Detailed asset info");
		final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
		scheduler.scheduleAtFixedRate(new StatusChange(jda), 0l, 1l, TimeUnit.MINUTES);
	}
}
