import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Pack, Sound, UploadSongService } from './upload-song.service';
import { Router } from '@angular/router';
import { ApiManagementService } from '../../../core/Services/api-management.service';
import { MatProgressSpinner } from '@angular/material/progress-spinner';
import {NgClass, NgForOf, NgIf} from '@angular/common';
import {FormsModule} from "@angular/forms";


@Component({
  selector: 'app-upload-song',
  standalone: true,
  imports: [
    MatProgressSpinner,
    NgClass,
    NgForOf,
    NgIf,
    FormsModule
  ],
  templateUrl: './upload-song.component.html',
  styleUrls: ['./upload-song.component.scss']
})
export class UploadSongComponent implements OnInit {

  constructor(
      private uploadSongService: UploadSongService,
      private apiService: ApiManagementService,
      private router: Router,
  ) { }

  public waitResponse: boolean = true;
  public showPreview: boolean = false;

  pack: Pack = {
    name: '',
    description: '',
    total_duration: '',
    genres: [],
    price: '',
    available_for: 'STANDARD',
    image: null,
    preview: '',
    paginated_sounds: []
  };

  newGenre: string = '';

  // Les indices correspondent aux sons dans this.pack.paginated_sounds
  newType: string[] = [];
  newSubtype: string[] = [];

  isDragOver: boolean = false;

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  ngOnInit() {
   this.waitResponse = true;
    this.apiService.get('api/user').subscribe((data: any | undefined) => {
      if (data && data[0] && data[0].roles === 'ADMIN') {
        this.waitResponse = false;
      } else {
        this.router.navigate(['/']);
      }
    },
    (error)=>{
      this.router.navigate(['/']);
    }
    );
  }

  // Méthode pour prévisualiser le fichier
  previewFile(input: any) {
    this.waitResponse = true;
    this.uploadSongService.previewPack(input).subscribe(
        (data: any | undefined) => {

          this.waitResponse = false;
          // Assigner les données reçues au pack et aux sons
          this.pack.name = data.pack.pack_name;
          this.pack.description = data.pack.description || '';
          this.pack.total_duration = data.pack.total_duration;
          this.pack.genres = data.pack.genres || [];
          this.pack.price = this.pack.price || '';
          this.pack.available_for = 'STANDARD'; // Valeur par défaut
          this.pack.preview = data.pack.preview || '';

          // Initialiser les tableaux newType et newSubtype
          this.newType = [];
          this.newSubtype = [];

          // Mapper les sons
          this.pack.paginated_sounds = data.audio.map((audio: any, index: number) => {
            // S'assurer que bpm est un nombre
            const bpm = audio.bpm ? Number(audio.bpm) : 0;

            // Ajouter des entrées pour newType et newSubtype
            this.newType[index] = '';
            this.newSubtype[index] = '';

            return {
              name: audio.song_name,
              duration_seconds: audio.duration_seconds || 0,
              bpm: bpm,
              key: audio.key || '',
              scale: audio.scale || '',
              type: audio.types || [],
              subtype: audio.subtypes || [],
              audio_file: typeof audio.audio_file === 'string' ? audio.audio_file : null,
              price: '1' // Prix par défaut
            } as Sound;
          });

          this.showPreview = true; // Afficher le bloc de prévisualisation
        },
        (error) => {
          this.waitResponse = false;
          console.error('Erreur lors de la prévisualisation du pack', error);
        }
    );
  }

  selectedFile(event: any) {
    const input = event.target.files[0];
    this.previewFile(input);
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragOver = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];
      this.previewFile(file);
      event.dataTransfer.clearData();
    }
  }

  // Gestion de l'upload

  onImageChange(event: any) {
    const file: File = event.target.files[0];
    this.pack.image = file;
  }

  addGenre() {
    if (this.newGenre && !this.pack.genres.includes(this.newGenre)) {
      this.pack.genres.push(this.newGenre);
      this.newGenre = '';
    }
  }

  removeGenre(genre: string) {
    this.pack.genres = this.pack.genres.filter(g => g !== genre);
  }

  addType(index: number) {
    const sound = this.pack.paginated_sounds[index];
    const typeToAdd = this.newType[index];
    if (typeToAdd && !sound.type.includes(typeToAdd)) {
      sound.type.push(typeToAdd);
      this.newType[index] = '';
    }
  }

  removeType(sound: Sound, type: string) {
    sound.type = sound.type.filter(t => t !== type);
  }

  addSubtype(index: number) {
    const sound = this.pack.paginated_sounds[index];
    const subtypeToAdd = this.newSubtype[index];
    if (subtypeToAdd && !sound.subtype.includes(subtypeToAdd)) {
      sound.subtype.push(subtypeToAdd);
      this.newSubtype[index] = '';
    }
  }

  removeSubtype(sound: Sound, subtype: string) {
    sound.subtype = sound.subtype.filter(s => s !== subtype);
  }

  async uploadPack() {
    this.waitResponse = true
    if (!this.pack.image) {
      this.waitResponse = false
      console.error('Image is required');
      return;
    }

    try {
      // Encoder l'image en base64
      const imageBase64 = await this.getBase64(this.pack.image);

      // Encoder tous les fichiers audio
      const sounds = await Promise.all(this.pack.paginated_sounds.map(async (sound) => {
        if (!sound.audio_file) {
          throw new Error(`Fichier audio pour ${sound.name} non fourni.`);
        }
        const audioBase64 = typeof sound.audio_file === 'string' ? sound.audio_file : await this.getBase64(sound.audio_file);
        return {
          ...sound,
          audio_file: audioBase64
        };
      }));

      const packData = {
        ...this.pack,
        image: imageBase64,
        sounds: sounds
      };

      this.uploadSongService.uploadPack(packData).subscribe(
          (response) => {
            this.resetPackData();
            this.showPreview = false;
            this.waitResponse = false;
          },
          (error) => {
            this.waitResponse = false;
          }
      );
    } catch (error) {
      this.waitResponse = false;
      console.error('Error encoding files', error);
    }
  }

  getBase64(file: File | string | null): Promise<string> {
    return new Promise((resolve, reject) => {
      if (!file) {
        resolve(''); // Résoudre avec une chaîne vide
      } else if (typeof file === 'string') {
        // Si c'est déjà une chaîne base64
        resolve(file);
      } else {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
          if (reader.result) {
            resolve(reader.result.toString());
          } else {
            reject(new Error('FileReader result is null'));
          }
        };
        reader.onerror = error => reject(error);
      }
    });
  }

  resetPackData() {
    this.pack = {
      name: '',
      description: '',
      total_duration: '',
      genres: [],
      price: '',
      available_for: 'STANDARD',
      image: null,
      preview:'',
      paginated_sounds: []
    };
    this.newGenre = '';
    this.newType = [];
    this.newSubtype = [];
    this.showPreview = false;
  }

}
