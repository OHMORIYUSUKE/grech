from fire import Fire
import sys
import pandas as pd

from termcolor import colored
from rich.console import Console

from grech.Views.ViewScore import ViewScore
from grech.Views.ViewResult import ViewResult
from grech.Views.ViewResultMdTable import ViewResultMdTable
from grech.UseCase.test.RunAllTest import RunAllTest
from grech.UseCase.score.TotallingScore import TotallingScore
from grech.UseCase.test.RunChapterTest import RunChapterTest


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
            print("見直しましょう。😭")
        else:
            print("よく頑張りました。🎉")

    def chapter(self, debug=0, name=""):
        """指定のチャプターが完了しているか確認します(--name チャプター名)"""
        print("実行中...")
        test_result_table_data = RunChapterTest().run_test_chapter(chapter_name=name)
        if test_result_table_data == None:
            print("指定のチャプターは存在しませんでした。😢")
            sys.exit(1)
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
            print("見直しましょう。😭")
        else:
            print("よく頑張りました。🎉")

    def report(self, name="all"):
        if name == "all":
            test_result_table_data = RunAllTest().run_test_all()
            md_table = ViewResultMdTable().view(
                test_result_table_data=test_result_table_data
            )
            html = md_table.to_html(index=False, border=0)
            print("===================ここから下のHTMLをコピーしてください===================")
            print(html)
        else:
            test_result_table_data = RunChapterTest().run_test_chapter(
                chapter_name=name
            )
            if test_result_table_data == None:
                print("指定のチャプターは存在しませんでした。😢")
                sys.exit(1)
            md_table = ViewResultMdTable().view(
                test_result_table_data=test_result_table_data
            )
            html = md_table.to_html(index=False, border=0)
            print("===================ここから下のHTMLをコピーしてください===================")
            print(html)
