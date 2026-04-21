# Password policies

The system enforces a default system-wide user password policy for local users. The password policy does not apply to users authenticated from remote directories.

The default password policy includes password aging rules, password complexity rules, password history, and user lockout rules. An admin user can update the default policy settings as needed. The default policy also applies to the admin user.

**Note:** Nokia recommends that system administrators configure a password policy for production deployments.

**Parent topic:** [Securing access to EDA](secure-access-eda.md)

## Modifying the default password policy <span id="modify-default-password-policy"></span>

/// html | div.steps

1. From the **System Administration** navigation panel, expand **USER MANAGEMENT**, click **Password Policy**, then click **Edit**.

    You can restore the default settings at this point or modify the password properties and lockout policy settings.

2. Modify any of the following password properties:

    - the minimum length of a password
    - the minimum number of lowercase characters
    - the minimum number of symbols or special characters
    - the number of passwords to keep and validate against
    - the minimum number of uppercase characters
    - the minimum number of numerical characters
    - whether the username can be used as a password
    - the duration, in days, for a password to remain valid
    - the hashing algorithm: **ARGON2** (the default), **PBKDF2-SHA512**, **PBKDF2-SHA256**, or **PBKDF2**

3. Modify any of the lockout policy settings:

    - the maximum consecutive failed login attempts before account lockout
    - duration, in seconds, to wait after reaching the maximum login failures before retry is allowed
    - whether to lock the account permanently after maximum number of failed logins
    - duration, in seconds, after which failed login attempts are reset

///
