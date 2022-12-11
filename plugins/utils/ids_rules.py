from pathlib import Path
import json
import math
import os
import logging

logger = logging.getLogger(__name__)


class IDSRules:
    def __init__(self):
        self.lines = 0
        self.event_count = 0
        self.user_agent_count = 0
        self.event_match = {}
        self.user_agent_match = {}

        self.attack_patterns = []

        self._prepare_ids_rules()

        # Remove duplicates from the patterns
        self.attack_patterns = set(self.attack_patterns)
        self.attack_patterns.remove("")

    def _prepare_ids_rules(self, pattern_dir=None):
        if not pattern_dir:
            pattern_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "ids_rules"
        for pattern_file in pattern_dir.iterdir():
            if pattern_file.is_dir():
                self._prepare_ids_rules(pattern_dir / pattern_file)
            elif str(pattern_file).endswith(".txt"):
                pattern = pattern_file.read_text()
                # Set text to lower case to not be case-sensitive
                self.attack_patterns.extend([p.strip() for p in pattern.splitlines()])

        self.idf_event, self.idf_max_event = self._calculate_idf(
            "term_frequency_event.json"
        )
        self.idf_user_agent, self.idf_max_user_agent = self._calculate_idf(
            "term_frequency_user_agent.json"
        )

    def _calculate_idf(self, file: str):
        """
        Calculate inverse document frequency from known frequency distribution.
        See: https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Inverse_document_frequency_2
        :param file:
        """

        term_frequency_file = (
            Path(os.path.dirname(os.path.abspath(__file__))) / f"ids_rules/{file}"
        )
        term_frequency_absolute = json.loads(
            term_frequency_file.read_text()
        )  # type: dict
        N = 1000000
        idf = {}
        for (term, num) in term_frequency_absolute.items():
            idf[term] = math.log(N / num)
        idf_max = max(idf.values())
        return idf, idf_max

    def _calculate_event_ids_score(self, p) -> float:
        """
        This function returns the tf-idf weight. In this function the term frequency
        is defined as either the term is in the document or not.
        See: https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency_2
        If the term was never seen before, it is weighted as very useful.
        So we give it twice the score as the highest idf weight.
        :param p: The pattern that was found
        :return: The score associated with the pattern
        """
        if p in self.idf_event:
            return self.idf_event[p]
        else:
            return 2 * self.idf_max_event

    def _calculate_user_agent_ids_score(self, p) -> float:
        """
        This function returns the tf-idf weight. In this function the term frequency
        is defined as either the term is in the document or not.
        See: https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency_2
        If the term was never seen before, it is weighted as very useful.
        So we give it twice the score as the highest idf weight.
        :param p: The pattern that was found
        :return: The score associated with the pattern
        """
        if p in self.idf_user_agent:
            return self.idf_user_agent[p]
        else:
            return 2 * self.idf_max_user_agent

    def ids_score(self, event: str, user_agent: str) -> int:
        event_exclude = {"&"}
        user_agent_exclude = {";", ".", "/", "(", ")", ",", ":"}
        score = 0

        self.lines += 1

        # Check how many patterns can be found in the event and user agent string
        for p in self.attack_patterns:
            if p not in event_exclude and p in event:
                score += self._calculate_event_ids_score(p)
                self.event_count += 1
                self._event_match(p)
            if p not in user_agent_exclude and p in user_agent:
                score += self._calculate_user_agent_ids_score(p)
                self.user_agent_count += 1
                self._user_agent_match(p)
        return score

    def _event_match(self, p: str):
        if p in self.event_match.keys():
            self.event_match[p] += 1
        else:
            self.event_match[p] = 1

    def _user_agent_match(self, p: str):
        if p in self.user_agent_match.keys():
            self.user_agent_match[p] += 1
        else:
            self.user_agent_match[p] = 1

    def print_ids_stats(self):
        logger.debug(f"IDS rules stat | Avg event: {self.event_count / self.lines}")
        logger.debug(
            f"IDS rules stat | Avg user agent: {self.user_agent_count / self.lines}"
        )
        logger.debug(f"IDS rules stat | Event match: {self.event_match}")
        logger.debug(f"IDS rules stat | User agent match: {self.user_agent_match}")


if __name__ == "__main__":
    utils = IDSRules()
    pass
