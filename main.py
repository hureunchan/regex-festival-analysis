from pathlib import Path
import re


def extract_data(text):
    # 1. 유효한 이메일 주소
    email_pattern = r"""
        (?<![A-Za-z0-9.!#$%&'*+/=?^_`{|}~-])
        [A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+
        @
        [A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?
        (?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+
        (?![A-Za-z0-9.-])
    """

    # 2. 010으로 시작하는 11자리 휴대폰 번호
    phone_pattern = r"(?<!\d)010[-. ]\d{4}[-. ]\d{4}(?!\d)"

    # 3. [학번 / 학과] 형식 중 202로 시작하는 9자리 학번
    student_pattern = r"\[(202\d{6})\s*/\s*([^\]]+)\]"

    # 4-1. github.com 저장소 주소 (gitlab.com 제외)
    github_pattern = r"https?://github\.com/[A-Za-z0-9_-]+/[A-Za-z0-9._-]+(?:\.git)?"

    # 4-2. 2026년에 발급된 쿠폰 코드
    coupon_pattern = r"\bFEST-2026-[A-Z0-9]{4}\b"

    # 5. '매출:' 바로 뒤에 나오는 부스별 총 매출액
    sales_pattern = r"매출:\s*([\d,]+)원"

    emails = re.findall(email_pattern, text, re.VERBOSE)
    phones = re.findall(phone_pattern, text)
    students = [
        (student_id, department.strip())
        for student_id, department in re.findall(student_pattern, text)
    ]
    github_urls = re.findall(github_pattern, text)
    coupons = re.findall(coupon_pattern, text)
    sales = [int(amount.replace(",", "")) for amount
             in re.findall(sales_pattern, text)]
    total_sales = sum(sales)

    return emails, phones, students, github_urls, coupons, sales, total_sales


def main():
    # 원본 로그 파일을 이 파이썬 파일과 같은 폴더에 data.txt로 저장하세요.
    file_path = Path(__file__).parent / "data.txt"

    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("data.txt 파일을 찾을 수 없습니다.")
        print("로그 파일을 이 프로그램과 같은 폴더에 두고 이름을 data.txt로 바꿔주세요.")
        return

    emails, phones, students, github_urls, coupons, sales, total_sales = extract_data(text)

    print("===== 1. 유효한 이메일 =====")
    for item in emails:
        print(item)

    print("\\n===== 2. 휴대폰 번호 =====")
    for item in phones:
        print(item)

    print("\\n===== 3. 학번과 학과 =====")
    for item in students:
        print(item)

    print("\\n===== 4. GitHub 저장소 URL =====")
    for item in github_urls:
        print(item)

    print("\\n===== 4. 2026년 유효 쿠폰 =====")
    for item in coupons:
        print(item)

    print("\\n===== 5. 부스별 총 매출 =====")
    for index, amount in enumerate(sales, start=1):
        print(f"{index}번 부스: {amount:,}원")

    print(f"전체 매출 합계: {total_sales:,}원")


if __name__ == "__main__":
    main()
