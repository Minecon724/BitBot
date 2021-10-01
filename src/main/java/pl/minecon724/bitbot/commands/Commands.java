package pl.minecon724.bitbot.commands;

import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class Commands extends ListenerAdapter {
	HelpCommand helpcmd = new HelpCommand();
	MarketCommand marketCmd = new MarketCommand();
	GiveawayCommand giveawayCmd;
	public Commands(GiveawayCommand gCmd) {
		this.giveawayCmd = gCmd;
	}

	public void onSlashCmd(SlashCommandEvent e) {
		switch (e.getName().toLowerCase()) {
		case "help":
			e.reply(helpcmd.process());
			break;
		case "money":
			break;
		case "exchange":
			break;
		case "market":
			e.replyEmbeds(marketCmd.process(e.getUser()));
			break;
		case "giveaway":
			break;
		}
	}
}
