from grech.Model.result.TestResultTable import TestResultTable
from grech.Model.result.ScoreTable import ScoreTable, ScoreRow


class TotallingScore:
    def __init__(self) -> None:
        pass

    def totalling_score(self, test_result_table_data: TestResultTable) -> ScoreTable:
        chapter_list = self.__get_chapter_list(
            test_result_table_data=test_result_table_data
        )
        pass_count = 0
        result_list = []
        for data in chapter_list:
            totalling_chapter_score_result = self.__totalling_chapter_score(
                chapter_name=data, test_result_table_data=test_result_table_data
            )
            result_list.append(totalling_chapter_score_result)
            if (
                totalling_chapter_score_result.score
                == totalling_chapter_score_result.max_score
            ):
                pass_count += 1
        all_pass_flag = False
        if pass_count == len(chapter_list):
            all_pass_flag = True
        return ScoreTable(result=result_list, status=all_pass_flag)

    def __totalling_chapter_score(
        self, chapter_name: str, test_result_table_data: TestResultTable
    ) -> ScoreRow:
        score = 0
        max_score = 0
        name_list = []
        for data in test_result_table_data.result:
            if data.chapter == chapter_name:
                max_score += 1
                if data.status == 1:
                    name_list.append(data.name)
                if data.status == 0:
                    score += 1
        return ScoreRow(
            chapter=chapter_name, name=name_list, score=score, max_score=max_score
        )

    def __get_chapter_list(self, test_result_table_data: TestResultTable) -> list:
        unique_list = []
        for data in test_result_table_data.result:
            unique_list.append(data.chapter)
        unique_list = sorted(set(unique_list), key=unique_list.index)
        return unique_list
