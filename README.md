# Docker Compose
```yaml
    api-user-manager:
        container_name: api-user-manager
        privileged: true
        ports:
            - '29573:29573'
        restart: always
        environment:
            TZ: "Asia/Seoul"
            PYTHONUNBUFFERED: 1
        logging:
            driver: "json-file"
            options:
                max-file: "5"
                max-size: "1m"
        volumes:
            - ./api-services/api-user-manager:/app
            - /var/log/api-user-manager/:/var/log/api-user-manager/
        networks:
            - 'core-net'
        build:
            context: ./api-services/api-user-manager/
        image: api-user-manager:0.3.1
```

## Version History
### `v0.2.0`
- 로그인, 로그아웃 시 사용 로그를 `스마트공장 1번가`로 전송하는 기능 추가
### `v0.2.1`
- API를 통한 관리자 계정 생성할 때, 기존 관리자 계정의 `access_token`을 확인하는 기능 추가
### `v0.2.2`
- 이미 로그인 되어 있는지 확인하는 api 추가
- access_token 없이 로그아웃 할 수 있도록 코드 수정
- auth_token api 추가
### `v0.2.3`
- 실제 로그인, 로그아웃 기록을 `스마트공장 1번가`로 전송하도록 변경
### `v0.3.0`
- 사용자 생성(회원가입), 기존 사용자 비밀번호 변경 시 비밀번호 validation 기능 추가 <br/>
  (최소 8자, 영어 대문자, 영어 소문자, 숫자, 특수문자 각 하나 이상 포함)
- 기존 로그인 성공 시 만료된 토큰이 반환되는 버그 수정
- 토큰 유효 기간 90일로 변경
### `v0.3.1`
- 토큰 검사 비활성화
- user object 반환 시 `password_hash` 제외하도록 수정