import {Component, Input} from '@angular/core';
import {PackService} from "../../../../core/Services/music/pack/pack.service";

@Component({
  selector: 'app-single-pack',
  standalone: true,
  imports: [],
  templateUrl: './single-pack.component.html',
  styleUrls: ['./single-pack.component.scss']
})
export class SinglePackComponent {
  @Input() id!: number;
  @Input() name: string = '';
  @Input() artist: string = '';
  @Input() genre: string[] = [];
  @Input() image: string = '';
  public isPlaying = false;

  constructor(private packService: PackService) {}

  togglePlay() {
    this.isPlaying = !this.isPlaying;
  }

  public getPackWithId() {
    if (this.id) {
      this.packService.getPackById(this.id).subscribe(
          (data: any) => {
            console.log("Détails du pack pour ID", this.id, ":", data);
          },
          error => {
            console.error("Erreur lors de la récupération du pack :", error);
          }
      );
    } else {
      console.warn("Aucun ID valide pour le pack");
    }
  }

}
