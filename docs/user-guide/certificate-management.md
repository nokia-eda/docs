# EDA certificate management

EDA plays the following roles in certificate management:

- Generates, signs, and distribute certificates, keys, and trust-bundles to EDA components and managed nodes
- Generates a root CA if no sub CA/CA provided during installation
- Generates a self-signed certificate for API/AS if no certificate is provided during installation; create a self-signed issuer to bootstrap a CA issuer
- Generates a certificate signing request (CSR) and sign certificates for nodes
- Generates a CSR and sign certificates for all EDA services

## Subtopics

- **[Trust bundles](trust-bundles.md)**  

- **[Certificate key pairs](certificate-key-pairs.md)**  

**Parent topic:** [Security](security.md)
