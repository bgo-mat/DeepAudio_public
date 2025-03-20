import { Component, ElementRef, OnInit, ViewChild, OnDestroy, Input } from '@angular/core';
import WaveSurfer from 'wavesurfer.js';
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {MusicCardService} from "./music-card.service";
import {Pack, Sound} from "../../models/pack.model";
import {CryptoUtilsService} from "../../../core/Services/crypto-utils.service";
import {AuthService} from "../../../core/Services/auth/auth.service";
import {PopupService} from "../auth-popup/auth-popup.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-music-card',
  templateUrl: './music-card.component.html',
  standalone: true,
  imports: [
    NgForOf,
    NgIf,
    NgClass,
  ],
  styleUrls: ['./music-card.component.scss']
})
export class MusicCardComponent implements OnInit, OnDestroy {
  @Input() sound: Sound | any;
  @ViewChild('waveform', { static: true }) waveformRef!: ElementRef;
  private wavesurfer!: WaveSurfer;
  public isPlaying: boolean = false;
  private audioUrl:string = "";

  isActive: boolean | undefined = false;
  isConnect: boolean = false;

  lastClickTime: number = 0;
  clickCooldown = 3000;
  creditStatus:number = 0;

  constructor(private musicCardService: MusicCardService,
              private encryptService :CryptoUtilsService,
              private authService: AuthService,
              private popupService: PopupService,
              public router: Router,) {
  }

  ngOnInit(): void {
    this.audioUrl = this.encryptService.decryptText(this.sound.audio_file) ;

    this.wavesurfer = WaveSurfer.create({
      container: this.waveformRef.nativeElement,
      waveColor: '#d1d1d1',
      progressColor: '#3b82f6',
      height: 40,
      barWidth: 2,
    });

    this.wavesurfer.load(this.audioUrl);

    this.wavesurfer.on('ready', () => {
      console.log('Waveform is ready');
    });

    this.wavesurfer.on('finish', () => {
      this.isPlaying = false;
    });

    this.isActive = this.sound?.is_favorite

    this.authService.getUserStatus().subscribe(status => {
      this.isConnect = status.isConnected;
      this.creditStatus = status.tokens;
    });
  }

  togglePlayPause(): void {
    this.wavesurfer.playPause();
    this.isPlaying = !this.isPlaying;
  }

  ngOnDestroy(): void {
    if (this.wavesurfer) {
      this.wavesurfer.destroy();
    }
  }

  formatDuration(duration: string): string {
    const parts = duration.split(':');
    const total = `${parts[1]}:${parts[2]}`;
    return total.split(".")[0]
  }

  addToFavorite(){
    if(this.isConnect){
      const currentTime = Date.now();
      this.isActive = !this.isActive
      if(this.sound && (currentTime - this.lastClickTime) > this.clickCooldown){
        if(this.sound.is_favorite){
          this.musicCardService.deleteTofavoriteCall(this.sound.id).subscribe(
              ()=>{
              },
              error=>{
                console.log(error)
              }
          )
        }else{
          this.musicCardService.addTofavoriteCall(this.sound.id).subscribe(
              ()=>{
              },
              error=>{
                console.log(error)
              }
          )
        }
      }
    }
    else{
      this.popupService.showPopup();
    }

  }

  buySong(){
    if(this.isConnect){
      const currentTime = Date.now();
      if(this.creditStatus < this.sound.price){
        this.popupService.showNoCreditsPopup();
      }else{
        if((currentTime - this.lastClickTime) > this.clickCooldown) {
          this.musicCardService.buySong(this.sound.id).subscribe(
              () => {
                document.location.reload()
              },
              error => {
                console.log(error)
              }
          )
        }
      }
      }
    else{
      this.popupService.showPopup();
    }
  }

  downloadSong(){
    const currentTime = Date.now();
    if (this.sound.is_buy && (currentTime - this.lastClickTime) > this.clickCooldown) {
      this.lastClickTime = currentTime;
      fetch(this.audioUrl)
          .then(response => response.blob())
          .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a: HTMLAnchorElement = document.createElement('a');
            a.href = url;
            a.download = `${this.sound.name}`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
          })
          .catch(error => console.error('Erreur lors du téléchargement :', error));
    }
  }

}
