package pl.minecon724.bitbot.utils;

public class Giveaway {
	int message;
	String prize;
	long ending;
	int winners;
	boolean ended;
	public Giveaway(int message, String prize, long ending, int winners) {
		this.message = message;
		this.prize = prize;
		this.ending = ending;
		this.winners = winners;
	}
	public String getPrize() {
		return prize;
	}
	public void setPrize(String prize) {
		this.prize = prize;
	}
	public long getEnding() {
		return ending;
	}
	public void setEnding(long ending) {
		this.ending = ending;
	}
	public int getWinners() {
		return winners;
	}
	public void setWinners(int winners) {
		this.winners = winners;
	}
	public boolean isEnded() {
		return ended;
	}
	public void setEnded(boolean ended) {
		this.ended = ended;
	}
}
