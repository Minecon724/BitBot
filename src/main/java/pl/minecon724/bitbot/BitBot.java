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
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;
import pl.minecon724.bitbot.commands.Commands;
import pl.minecon724.bitbot.commands.GiveawayCommand;
import pl.minecon724.bitbot.listeners.EventReady;
import pl.minecon724.bitbot.utils.EcoManager;
import pl.minecon724.bitbot.utils.StatusChange;

public class BitBot {
	static EcoManager ecoMan;
	static GiveawayCommand giveaway;
	
	public static void main(String[] args) throws LoginException, ClassNotFoundException, SQLException {
		giveaway = new GiveawayCommand(args[2]);
		//ecoMan = new EcoManager(args[1]);
		JDA jda = JDABuilder.createDefault(args[0]).build();
		jda.addEventListener(new EventReady());
		jda.addEventListener(new Commands(giveaway));
		jda.upsertCommand("help", "Show all commands");
		CommandData exchangeCmd = new CommandData("exchange", "Exchange assets");
		exchangeCmd.addOption(OptionType.STRING, "From", "Asset you want to sell");
		exchangeCmd.addOption(OptionType.STRING, "To", "Asset you want to buy");
		exchangeCmd.addOption(OptionType.INTEGER, "Quantity", "Quantity of the asset you want to SELL");
		jda.upsertCommand(exchangeCmd);
		CommandData marketCmd = new CommandData("market", "View market");
		marketCmd.addOption(OptionType.STRING, "Asset", "Detailed asset info", false);
		jda.upsertCommand(marketCmd);
		jda.upsertCommand("money", "Check account balance");
		CommandData giveawayCmd = new CommandData("giveaway", "Giveaway commands");
		SubcommandData gStart = new SubcommandData("start", "Start a giveaway");
		gStart.addOption(OptionType.INTEGER, "winners", "winner count");
		gStart.addOption(OptionType.INTEGER, "minutes", "d");
		gStart.addOption(OptionType.STRING, "prize", "g");
		giveawayCmd.addSubcommands(gStart);
		SubcommandData gReroll = new SubcommandData("reroll", "Reroll winner");
		gReroll.addOption(OptionType.INTEGER, "message id", "Giveaway message id");
		giveawayCmd.addSubcommands(gReroll);
		SubcommandData gEnd = new SubcommandData("end", "End giveaway");
		gEnd.addOption(OptionType.INTEGER, "message id", "Giveaway message id");
		giveawayCmd.addSubcommands(gEnd);
		final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
		scheduler.scheduleAtFixedRate(new StatusChange(jda), 0l, 1l, TimeUnit.MINUTES);
		scheduler.scheduleAtFixedRate(giveaway.new refresh(), 0l, 1l, TimeUnit.MINUTES);
	}
}
