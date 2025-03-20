// src/app/utils/cryptoUtils.service.ts

import { Injectable } from '@angular/core';
import CryptoJS from 'crypto-js';

@Injectable({
  providedIn: 'root'
})
export class CryptoUtilsService {

  constructor() { }

  private ENCRYPTION_KEY = "Smj5282Lr1oH8xjn080S99YVw39o4iYp1Q014GCjY2A=";
  private key = CryptoJS.enc.Base64.parse(this.ENCRYPTION_KEY);

  decryptText(cipherText: string): string {
    try {
      // Décoder le texte chiffré en Base64
      const cipherBytes = CryptoJS.enc.Base64.parse(cipherText);

      // Extraire l'IV (les 16 premiers octets)
      const iv = CryptoJS.lib.WordArray.create(cipherBytes.words.slice(0, 4), 16); // 4 mots * 4 octets = 16 octets

      // Extraire le ciphertext (le reste des octets)
      const ciphertext = CryptoJS.lib.WordArray.create(cipherBytes.words.slice(4), cipherBytes.sigBytes - 16);

      // Créer un objet CipherParams avec le ciphertext
      const cipherParams = CryptoJS.lib.CipherParams.create({
        ciphertext: ciphertext
      }) as CryptoJS.lib.CipherParams;

      // Déchiffrer le ciphertext avec la clé et l'IV
      const decrypted = CryptoJS.AES.decrypt(
          cipherParams,
          this.key,
          {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7,
          }
      );

      // Convertir les données déchiffrées en chaîne UTF-8
      return decrypted.toString(CryptoJS.enc.Utf8);
    } catch (error) {
      console.error('Erreur de déchiffrement:', error);
      return '';
    }
  }
}
