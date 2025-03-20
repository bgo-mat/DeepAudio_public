import { Component, Input } from '@angular/core';
import { Pack } from '../../../models/pack.model';
import {NgForOf, NgIf} from "@angular/common";

@Component({
  selector: 'app-pack-info',
  templateUrl: './pack-info.component.html',
  styleUrls: ['./pack-info.component.scss'],
  standalone: true,
  imports: [
    NgIf,
    NgForOf
  ],
})
export class PackInfoComponent {
  @Input() pack: Pack | null = null;
  public isPlaying = false;

  togglePlay(event: Event): void {
    event.stopPropagation();
    this.isPlaying = !this.isPlaying;
  }
}
