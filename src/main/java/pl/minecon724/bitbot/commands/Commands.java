package pl.minecon724.bitbot.commands;

import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import pl.minecon724.bitbot.BitBot;

public class Commands extends ListenerAdapter {
	BitBot bitbot;
	HelpCommand helpcmd = new HelpCommand();
	public Commands(BitBot bitbot) {
		this.bitbot = bitbot;
	}

	public void onSlashCmd(SlashCommandEvent e) {
		if (e.getName().equalsIgnoreCase("help")) {
			e.reply(helpcmd.process());
		}
	}
}
