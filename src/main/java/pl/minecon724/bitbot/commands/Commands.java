package pl.minecon724.bitbot.commands;

import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

public class Commands extends ListenerAdapter {
	HelpCommand helpcmd = new HelpCommand();

	public void onSlashCmd(SlashCommandEvent e) {
		if (e.getName().equalsIgnoreCase("help")) {
			e.reply(helpcmd.process());
		}
	}
}
