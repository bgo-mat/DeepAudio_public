import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {Pack} from "../../shared/models/pack.model";
import {PackService} from "../../core/Services/music/pack/pack.service";
import {PackInfoComponent} from "../../shared/components/detail-pack/pack-info/pack-info.component";
import {FilterSoundsComponent} from "../../shared/components/filter/filter-sounds/filter-sounds.component";
import {HeaderMusicComponent} from "../../shared/components/header-music/header-music.component";
import {MusicCardComponent} from "../../shared/components/music-card/music-card.component";
import {NgForOf} from "@angular/common";

@Component({
    selector: 'app-pack-detail',
    templateUrl: './pack-detail.component.html',
    styleUrls: ['./pack-detail.component.scss'],
    standalone: true,
    imports: [
        PackInfoComponent,
        FilterSoundsComponent,
        HeaderMusicComponent,
        MusicCardComponent,
        NgForOf,
        // Vos imports de composants
    ],
})
export class PackDetailComponent implements OnInit {
    pack: Pack | null = null;
    packId: number | null = null;

    constructor(
        private route: ActivatedRoute,
        private packService: PackService
    ) {}

    ngOnInit(): void {
        const idParam = this.route.snapshot.paramMap.get('id');
        this.packId = idParam !== null ? Number(idParam) : null;

        if (this.packId !== null) {
            this.fetchPackDetails(this.packId);
        } else {
            console.error("Aucun ID de pack fourni dans l'URL");
        }
    }

    fetchPackDetails(packId: number): void {
        this.packService.getPackById(packId).subscribe(
            (pack) => {
                this.pack = pack;
                console.log('Pack chargé dans PackDetailComponent :', this.pack);
            },
            (error) => {
                console.error('Erreur lors de la récupération du pack :', error);
            }
        );
    }
}
