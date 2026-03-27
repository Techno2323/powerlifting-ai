import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)


# ── Score Calculator ──────────────────────────────────────────────────────────

class ScoreCalculator:
    """Calculates a session score out of 100 based on completion, weight logging, and RPE."""

    # Point allocations (magic numbers explained)
    _COMPLETION_PTS = 50   # Marking a session complete
    _WEIGHTS_PTS    = 20   # Logging actual weights used
    _RPE_MAX_PTS    = 30   # Max RPE contribution (scaled: rpe/10 * 30)

    def calculate(self, completed: bool, rpe: float, weights_entered: bool) -> int:
        """
        Score a session out of 100:
          - Marking complete:     50 pts
          - Logging weights:      20 pts
          - RPE contribution:     up to 30 pts  (scaled: rpe/10 * 30)

        A perfect session (complete + weights + RPE 10) = 100.
        """
        score = 0
        if completed:
            score += self._COMPLETION_PTS
        if weights_entered:
            score += self._WEIGHTS_PTS
        if rpe > 0:
            score += min(int((rpe / 10) * self._RPE_MAX_PTS), self._RPE_MAX_PTS)
        logger.debug("calculate_score: completed=%s rpe=%s weights=%s -> %d", completed, rpe, weights_entered, score)
        return score


# ── Progress Calculator ───────────────────────────────────────────────────────

class ProgressCalculator:
    """Derives progress metrics from a session list and a workout log dict."""

    def calculate(self, all_sessions: list, log: dict) -> tuple:
        """
        Returns (total_completed, total_sessions, overall_progress_pct, total_score).

        *all_sessions* — list of session dicts from :func:`ScheduleBuilder.build`.
        *log*          — {session_id: log_row} dict from the database.
        """
        total_sessions = len(all_sessions)
        if total_sessions == 0:
            logger.debug("calculate_progress: no sessions")
            return 0, 0, 0, 0

        completed   = [s for s in all_sessions if log.get(s["session_id"], {}).get("completed")]
        total_score = sum(log.get(s["session_id"], {}).get("score", 0) for s in all_sessions)
        pct         = int((len(completed) / total_sessions) * 100)

        logger.debug(
            "calculate_progress: %d/%d completed (%d%%), score=%d",
            len(completed), total_sessions, pct, total_score,
        )
        return len(completed), total_sessions, pct, total_score


# ── Schedule Builder ──────────────────────────────────────────────────────────

class ScheduleBuilder:
    """Maps training plan days to calendar dates."""

    def build(self, plan: dict, start_date: date) -> list:
        """
        Map each training day in the plan to a calendar date.
        Uses evenly spaced gaps: gap = 7 // training_days days between sessions.
        """
        sessions = []
        current_date = start_date
        training_days = plan.get("training_days", 3)
        # at least 1 day gap to avoid ZeroDivisionError
        gap = max(1, 7 // training_days)

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

        logger.debug("build_session_schedule: %d sessions built", len(sessions))
        return sessions

    def get_today_session(self, all_sessions: list, log: dict):
        """
        Return the most relevant session for today.

        Priority:
          1. A session whose calendar date is exactly today.
          2. The earliest upcoming unlogged session (lets users catch up).
          3. None (everything done or all in the future).
        """
        today_str = str(date.today())

        for s in all_sessions:
            if s["date"] == today_str:
                return s

        for s in all_sessions:
            if s["date"] >= today_str and s["session_id"] not in log:
                return s

        return None


# ── Module-level singletons ───────────────────────────────────────────────────

_score_calc    = ScoreCalculator()
_progress_calc = ProgressCalculator()
_schedule      = ScheduleBuilder()


# ── Backward-compatible module-level functions ────────────────────────────────

def calculate_score(completed: bool, rpe: float, weights_entered: bool) -> int:
    return _score_calc.calculate(completed, rpe, weights_entered)


def calculate_progress(all_sessions: list, log: dict) -> tuple:
    return _progress_calc.calculate(all_sessions, log)


def build_session_schedule(plan: dict, start_date: date) -> list:
    return _schedule.build(plan, start_date)


def get_today_session(all_sessions: list, log: dict):
    return _schedule.get_today_session(all_sessions, log)