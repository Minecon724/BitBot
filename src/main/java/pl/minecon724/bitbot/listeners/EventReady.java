package pl.minecon724.bitbot.listeners;

import net.dv8tion.jda.api.events.GenericEvent;
import net.dv8tion.jda.api.events.ReadyEvent;
import net.dv8tion.jda.api.hooks.EventListener;
import pl.minecon724.bitbot.BitBot;

public class EventReady implements EventListener {
	BitBot bitbot;
	public EventReady(BitBot bitbot) {
		this.bitbot = bitbot;
	}
	@Override
    public void onEvent(GenericEvent event) {
		if (event instanceof ReadyEvent) System.out.println("BitBot wystarowal!");
	}
}
