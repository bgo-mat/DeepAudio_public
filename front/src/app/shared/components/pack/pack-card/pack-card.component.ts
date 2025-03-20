import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-pack-card',
  templateUrl: './pack-card.component.html',
  standalone: true,
  styleUrls: ['./pack-card.component.scss']
})
export class PackCardComponent {
 @Input() pack: any;

  public isPlaying = false;

  togglePlay(event: Event): void {
    event.stopPropagation();
    this.isPlaying = !this.isPlaying;
  }
}
