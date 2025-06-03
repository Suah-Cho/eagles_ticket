import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# 크롬 옵션 설정
# options = Options()
# options.add_argument("user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data")
# options.add_argument("profile-directory=Default")

# 크롬 드라이버 서비스 설정
service = Service()

def wait_until_captcha_passed(driver):
    print("보안문자를 직접 입력하고, '입력완료' 버튼을 누르세요.")
    try:
        # '다음단계' 버튼이 활성화되는 시점을 기다림 (예시: class 변경 or 등장)
        WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '다음단계')]"))
        )
        print("보안문자 통과 감지됨. 다음 단계로 진행합니다.")
    except Exception as e:
        print(f"보안문자 통과 실패 또는 시간 초과: {e}")

def click_reserve_button(driver):
    # 예매하기 버튼 찾기 및 클릭
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='date_num' and text()='06.10']/ancestor::li//a[contains(@class, 'btn btn_reserve')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    driver.execute_script("arguments[0].click();", button)
    print("06.16 예매하기 버튼 클릭 완료.")

    confirm_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "common_modal_close"))
    )
    confirm_button.click()
    print("예매 안내 팝업 닫기 완료.")

def navigate_to_ticket_page(driver):
    # LG 예매
    ticket_page_url = "https://www.ticketlink.co.kr/sports/137/63"


    driver.get(ticket_page_url)

    try:
        # 예약 페이지 로딩 대기
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "planTitle"))  # 예약 페이지의 특정 요소 class로 변경
        )
        print("예약 페이지 접근 성공.")
    except Exception as e:
        print(f"예약 페이지 접근 오류 발생: {e}")


def setup_driver():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    return driver


def login_to_payco(driver):
    # PAYCO 로그인 페이지로 이동
    login_url = "https://id.payco.com/oauth2.0/authorize?serviceProviderCode=TKLINK&scope=&response_type=code&state=552be1ed1114458787d51df604dfdc44&client_id=Z9Ur2WLH9rB59Gy4_cJ3&redirect_uri=https://www.ticketlink.co.kr/auth/callback?selfRedirect=N&userLocale=ko_KR"
    driver.get(login_url)

    try:
        # 로그인 폼 로딩 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "id"))
        )

        # 로그인 정보 입력
        driver.find_element(By.ID, "id").send_keys("sisterjosua@naver.com")  # 사용자 ID 입력
        driver.find_element(By.ID, "pw").send_keys("qawsed70!")  # 사용자 비밀번호 입력

        # 로그인 버튼 클릭
        login_button = driver.find_element(By.ID, "loginButton")
        login_button.click()

        # 로그인 완료 대기 (로그인 후 나타나는 요소 ID로 변경 필요)
        # WebDriverWait(driver, 2).until(
        #     EC.presence_of_element_located((By.ID, "some_element_after_login"))
        # )

        print("로그인 성공.")
    except Exception as e:
        print(f"로그인 오류 발생: {e}")


def main():
    driver = setup_driver()

    try:
        login_to_payco(driver)  # PAYCO 로그인
        input("로그인 후 엔터 키를 누르세요...")  # 로그인 완료 후 대기
        navigate_to_ticket_page(driver)  # 티켓 페이지로 이동
        click_reserve_button(driver)  # 예매하기 버튼 클릭
        wait_until_captcha_passed(driver)  # 보안문자 입력 대기

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        input("창을 닫으려면 엔터 키를 누르세요...")
        driver.quit()


if __name__ == "__main__":
    main()