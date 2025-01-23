import time
import pandas as pd
import numpy as np

# 도시 이름을 키로 하고 해당 도시의 데이터 파일 경로를 값으로 하는 딕셔너리
도시_데이터 = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def 필터_가져오기():
    """
    사용자로부터 분석할 도시, 월, 요일을 입력받습니다.

    Returns:

        도시 (str): 분석할 도시 이름
        월 (str): 필터링할 월 이름 또는 "all" (모든 월)
        요일 (str): 필터링할 요일 이름 또는 "all" (모든 요일)
    
    """
    print('안녕! 미국 자전거 공유 데이터를 탐색해보자!')

    # 도시 이름 입력받기
    도시 = ""
    도시_이름들 = list(도시_데이터.keys())

    while 도시 not in 도시_이름들:
        도시 = input(f"분석할 도시 이름을 입력하세요 {도시_이름들}: ").lower()

    # 월 입력받기
    월 = ""
    유효한_월 = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
               'july', 'august', 'september', 'october', 'november', 'december']

    while 월 not in valid_월:
        월 = input("필터링할 월을 입력하세요 (예: 'all', 'january' ... 'december'): ").lower()

    # 요일 입력받기
    요일 = ""
    유효한_요일 = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while 요일 not in 유효한_요일:
        요일 = input("필터링할 요일을 입력하세요 (예: 'all', 'monday' ... 'sunday'): ").lower()

    print(f"\n입력한 값 - 도시: '{도시}', 월: '{월}', 요일: '{요일}'")
    print('-'*40)

    return 도시, 월, 요일

def 데이터_불러오기(도시, 월, 요일):
    """
    지정된 도시의 데이터를 불러오고, 선택한 월과 요일로 필터링합니다.

    Args:
        도시 (str): 분석할 도시 이름
        월 (str): 필터링할 월 이름 또는 "all"
        요일 (str): 필터링할 요일 이름 또는 "all"
    Returns:
        데이터프레임 (DataFrame): 필터링된 데이터프레임
    """
    파일_경로 = 도시_데이터[도시]
    데이터 = pd.read_csv(파일_경로)

    데이터['시작시간'] = pd.to_datetime(데이터['Start Time'])
    데이터['월'] = 데이터['시작시간'].dt.strftime('%B').str.lower()
    데이터['요일'] = 데이터['시작시간'].dt.day_name().str.lower()

    if 월 != 'all':
        데이터 = 데이터[데이터['월'] == 월]

    if 요일 != 'all':
        데이터 = 데이터[데이터['요일'] == 요일]

    return 데이터

def 시간_통계(데이터):
    """가장 빈번한 여행 시간에 대한 통계를 계산합니다."""
    print('\n가장 빈번한 여행 시간 통계를 계산 중입니다...\n')
    시작시간 = time.time()

    가장_흔한_월 = 데이터['월'].mode()[0]
    print(f"가장 흔한 월은: {가장_흔한_월}")

    가장_흔한_요일 = 데이터['요일'].mode()[0]
    print(f"가장 흔한 요일은: {가장_흔한_요일}")

    데이터['시간'] = 데이터['시작시간'].dt.hour
    가장_흔한_시간 = 데이터['시간'].mode()[0]
    print(f"가장 흔한 시간은: {가장_흔한_시간}시")

    print(f"\n이 통계를 계산하는 데 {time.time() - 시작시간:.4f}초가 걸렸습니다.")
    print('-'*40)

def 역_통계(데이터):

    print('\n가장 인기 있는 출발지와 도착지, 그리고 여행 경로 통계를 계산 중입니다...\n')
    시작시간 = time.time()

    가장_많이_사용된_출발지 = 데이터['Start Station'].mode()[0]
    print(f"가장 많이 사용된 출발지는: {가장_많이_사용된_출발지}")

    가장_많이_사용된_도착지 = 데이터['End Station'].mode()[0]
    print(f"가장 많이 사용된 도착지는: {가장_많이_사용된_도착지}")

    출발_도착_조합 = 데이터['Start Station'] + " -> " + 데이터['End Station']
    가장_흔한_조합 = 출발_도착_조합.mode()[0]
    print(f"가장 빈번한 출발지와 도착지 조합은: {가장_흔한_조합}")

    print(f"\n이 통계를 계산하는 데 {time.time() - 시작시간:.4f}초가 걸렸습니다.")
    print('-'*40)

def 여행시간_통계(데이터):
    """총 여행 시간과 평균 여행 시간에 대한 통계를 계산합니다."""
    print('\n여행 시간 통계를 계산 중입니다...\n')
    시작시간 = time.time()

    총_여행시간 = 데이터['Trip Duration'].sum()
    평균_여행시간 = 데이터['Trip Duration'].mean()

    총_시간, 총_분, 총_초 = 시간_변환(총_여행시간)
    평균_시간, 평균_분, 평균_초 = 시간_변환(평균_여행시간)

    print(f"총 여행 시간은 {총_시간}시간 {총_분}분 {총_초}초입니다.")
    print(f"평균 여행 시간은 {평균_시간}시간 {평균_분}분 {평균_초}초입니다.")

    print(f"\n이 통계를 계산하는 데 {time.time() - 시작시간:.4f}초가 걸렸습니다.")
    print('-'*40)

def 시간_변환(초):
    """초를 시, 분, 초로 변환합니다."""
    시간 = int(초 // 3600)
    분 = int((초 % 3600) // 60)
    초 = round(초 % 60, 2)
    return 시간, 분, 초

def 사용자_통계(데이터):
    """사용자 유형, 성별, 출생 연도에 대한 통계를 계산합니다."""
    print('\n사용자 통계를 계산 중입니다...\n')
    시작시간 = time.time()

    사용자_유형 = 데이터['User Type'].value_counts()
    print("사용자 유형별 개수:")
    print(user_type_counts)

    if 'Gender' in 데이터.columns:
        성별_정보 = 데이터['Gender'].value_counts()
        print("성별별 개수:")
        print(성별_정보)
    else:
        print("성별 데이터가 없습니다.")

    if 'Birth Year' in 데이터.columns:
        가장_오래된_출생연도 = int(데이터['Birth Year'].min())
        print(f"가장 오래된 출생 연도: {가장_오래된_출생연도}")

        가장_최근_출생연도 = int(데이터['Birth Year'].max())
        print(f"가장 최근 출생 연도: {가장_최근_출생연도}")

        가장_흔한_출생연도 = int(데이터['Birth Year'].mode()[0])
        print(f"가장 흔한 출생 연도: {가장_흔한_출생연도}")
    else:
        print("출생 연도 데이터가 없습니다.")

    print(f"\n이 통계를 계산하는 데 {time.time() - 시작시간:.4f}초가 걸렸습니다.")
    print('-'*40)

def 원시데이터_표시(데이터):
    """
    사용자 요청에 따라 원시 데이터를 5행씩 출력합니다.
    """
    시작_행 = 0
    while True:
        표시_요청 = input("\n원시 데이터를 5행씩 더 보고 싶으신가요? 'yes' 또는 'no'로 입력하세요: ").lower()
        if 표시_요청 == 'yes':
            print(데이터.iloc[시작_행:시작_행 + 5])
            시작_행 += 5
        elif 표시_요청 == 'no':
            print("\n원시 데이터 표시를 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 'yes' 또는 'no'로 입력해주세요.")

def main():
    """주요 프로그램 실행 루프"""
    while True:
        도시, 월, 요일 = 필터_가져오기()
        데이터 = 데이터_불러오기(도시, 월, 요일)

        if 데이터.empty:
            print("입력한 조건에 맞는 데이터가 없습니다.")
        else:
            원시데이터_표시(데이터)
            시간_통계(데이터)
            역_통계(데이터)
            여행시간_통계(데이터)
            사용자_통계(데이터)

        다시시작 = input('\n다시 시작하시겠습니까? "yes" 또는 "no"를 입력하세요.\n').lower()
        if 다시시작 != 'yes':
            print("프로그램을 종료합니다. 감사합니다!")
            break

if __name__ == "__main__":
    main()
