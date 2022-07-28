from fire import Fire
import sys
from termcolor import colored
from rich.console import Console

from os_lecture_support_tool.UseCase.config.ReadConfig import ReadConfig
from os_lecture_support_tool.Views.ViewConfig import ViewConfig
from os_lecture_support_tool.Views.ViewScore import ViewScore
from os_lecture_support_tool.Views.ViewResult import ViewResult

from os_lecture_support_tool.UseCase.test.RunAllTest import RunAllTest

from os_lecture_support_tool.UseCase.score.TotallingScore import TotallingScore
from os_lecture_support_tool.UseCase.test.RunChapterTest import RunChapterTest
from os_lecture_support_tool.UseCase.config.SetConfig import SetConfig


class Config:
    """設定を行います。"""

    def set(self, file=""):
        """チェックする項目が記載されたYAMLファイルの場所を設定します。 --set {URL}"""
        print("入力しない場合は、デフォルト値または、すでに設定されている値になります。")
        SetConfig().check_exist_config_file(file_path=file)
        user_config_list = ReadConfig().read_config_all()
        table = ViewConfig().view(user_config_list=user_config_list)
        console = Console()
        console.print(table)
        print("上記の内容で、設定を保存しました。")

    def check(self):
        try:
            user_config_list = ReadConfig().read_config_all()
            table = ViewConfig().view(user_config_list=user_config_list)
            console = Console()
            console.print(table)
        except:
            print(colored("設定がされていません。", "red"))
            sys.exit(1)


class Check:
    """課題の状態を確認することができます。"""

    def all(self, debug=0):
        """すべての課題が終了しているか確認します。"""
        print("実行中...")
        test_result_table_data = RunAllTest().run_test_all()
        if debug == 1:
            table = ViewResult(debug_mode=True).view(
                test_result_table_data=test_result_table_data
            )
        else:
            table = ViewResult(debug_mode=False).view(
                test_result_table_data=test_result_table_data
            )
        console = Console()
        console.print(table)
        # スコア
        score_table_data = TotallingScore().totalling_score(
            test_result_table_data=test_result_table_data
        )
        score_table = ViewScore().view(score_table_data=score_table_data)
        console = Console()
        console.print(score_table)
        if score_table_data.status == False:
            print("見直しましょう。")
        else:
            print("よく頑張りました。")

    def chapter(self, name="", debug=0):
        """指定のチャプターが完了しているか確認します(--name チャプター名)"""
        print("実行中...")
        test_result_table_data = RunChapterTest().run_test_chapter(chapter_name=name)
        if debug == 1:
            table = ViewResult(debug_mode=True).view(
                test_result_table_data=test_result_table_data
            )
        else:
            table = ViewResult(debug_mode=False).view(
                test_result_table_data=test_result_table_data
            )
        console = Console()
        console.print(table)
        # スコア
        score_table_data = TotallingScore().totalling_score(
            test_result_table_data=test_result_table_data
        )
        score_table = ViewScore().view(score_table_data=score_table_data)
        console = Console()
        console.print(score_table)
        if score_table_data.status == False:
            print("見直しましょう。")
        else:
            print("よく頑張りました。")


class Command:
    config = Config
    check = Check


def main():
    Fire(Command)


if __name__ == "__main__":
    main()
