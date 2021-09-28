package pl.minecon724.bitbot.utils;

import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.Activity;

public class StatusChange implements Runnable {
	JDA jda;
	public StatusChange(JDA jda) {
		this.jda = jda;
	}
	@Override
	public void run() {
		jda.getPresence().setActivity(Activity.playing("Na " + jda.getGuilds().size() + "serwerach!"));
	}

}
