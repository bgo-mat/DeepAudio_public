export interface Pack {
    id: number;
    name: string;
    description: string;
    duration: string;
    num_sounds: number;
    price: string;
    genre_name: string[];
    labels: string[];
    image: string;
    available_for: string;
    preview: string;
    is_favorite: boolean;
    paginated_sounds: Sound[];
}

export interface Sound {
    id: number;
    pack: number;
    name: string;
    price: string;
    key: string;
    scale: string;
    bpm: number;
    duration: string;
    type_names: string;
    subtype_names: string;
    audio_file: string;
    available_for: string;
    image: string;
    is_buy:boolean,
    is_favorite:boolean
}
