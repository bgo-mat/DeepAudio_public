import { Component, OnInit } from '@angular/core';
import { Pack } from '../../../models/pack.model';
import { SinglePackComponent } from "../single-pack/single-pack.component";
import { PackService } from '../../../../core/Services/music/pack/pack.service';
import { CommonModule } from "@angular/common";

@Component({
  selector: 'app-most-recent',
  templateUrl: './most-recent-pack.component.html',
  standalone: true,
  imports: [
    SinglePackComponent,
    CommonModule
  ],
  styleUrls: ['./most-recent-pack.component.scss']
})
export class MostRecentPackComponent implements OnInit {
  packs: Pack[] = [];

  constructor(private packService: PackService) {}

  ngOnInit(): void {
    this.packService.getPacks('created_at').subscribe(
        (data: any) => {
          console.log("PIPI", data)
          this.packs = data.results.map((item: any) => ({
            id: item.id,
            name: item.name,
            genre: item.genre_names[0],
            image: 'assets/test.png' || 'assets/default-pack-image.png'
          }));
        },
        error => {
          console.error('Erreur lors du chargement des packs récents:', error);
        }
    );
    console.log(this.packs)
  }
}
