from datetime import date, timedelta


def calculate_score(completed: bool, rpe: float, weights_entered: bool) -> int:
    """
    Score a session out of 100:
      - Marking complete:     50 pts
      - Logging weights:      20 pts
      - RPE contribution:     up to 30 pts  (scaled: rpe/10 * 30)

    This keeps the max honest — a perfect session (complete + weights + RPE 10) = 100.
    """
    score = 0
    if completed:
        score += 50
    if weights_entered:
        score += 20
    if rpe > 0:
        score += min(int((rpe / 10) * 30), 30)
    return score


def build_session_schedule(plan: dict, start_date: date) -> list[dict]:
    """
    Map each training day in the plan to a calendar date.
    Uses evenly spaced gaps: gap = 7 // training_days days between sessions.
    """
    sessions = []
    current_date = start_date
    training_days = plan.get("training_days", 3)
    gap = max(1, 7 // training_days)  # at least 1 day gap, avoid ZeroDivisionError

    for week in plan.get("weeks", []):
        for day in week.get("days", []):
            sessions.append({
                "session_id":  f"w{week['week']}_d{day['day_number']}",
                "week":        week["week"],
                "week_focus":  week.get("focus", ""),
                "label":       day.get("label", f"Day {day['day_number']}"),
                "exercises":   day.get("exercises", []),
                "date":        str(current_date),
            })
            current_date += timedelta(days=gap)

    return sessions


def get_today_session(all_sessions: list[dict], log: dict) -> dict | None:
    """
    Priority:
      1. A session whose calendar date is exactly today.
      2. The earliest upcoming unlogged session (lets users catch up).
      3. None (everything done or all in the future).
    """
    today_str = str(date.today())

    # Exact date match first
    for s in all_sessions:
        if s["date"] == today_str:
            return s

    # Next incomplete session on or after today
    for s in all_sessions:
        if s["date"] >= today_str and s["session_id"] not in log:
            return s

    return None


def calculate_progress(all_sessions: list[dict], log: dict) -> tuple[int, int, int, int]:
    """
    Returns (total_completed, total_sessions, overall_progress_pct, total_score).
    """
    total_sessions = len(all_sessions)
    if total_sessions == 0:
        return 0, 0, 0, 0

    completed   = [s for s in all_sessions if log.get(s["session_id"], {}).get("completed")]
    total_score = sum(log.get(s["session_id"], {}).get("score", 0) for s in all_sessions)
    pct         = int((len(completed) / total_sessions) * 100)

    return len(completed), total_sessions, pct, total_score