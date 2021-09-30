package pl.minecon724.bitbot.commands;

import java.time.Instant;

import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.MessageEmbed;
import net.dv8tion.jda.api.entities.User;

public class MarketCommand {
	
	public MessageEmbed process(User executor) {
		EmbedBuilder embed = new EmbedBuilder();
		embed.setTitle("Market");
		embed.addField("soon", "tm", false);
		embed.setTimestamp(Instant.now());
		embed.setFooter(executor.getAsTag(), executor.getEffectiveAvatarUrl());
		embed.setColor(0xFFFFFF);
		return embed.build();
	}
}
