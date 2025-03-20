import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ParamsService } from "./params.service";

export type queryParams = { [param: string]: string | number | boolean | ReadonlyArray<string | number | boolean> }

@Injectable({
    providedIn: 'root'
})
export class ApiManagementService {

    constructor(private _http: HttpClient, private paramsService: ParamsService) {}

    get<T>(path: string, options: {
        params?: queryParams,
        error_message?: string,
        call_without_token?: boolean,
        force?: boolean
    } = {}): Observable<T> {
        return this._http.get<T>(
            this.paramsService.url_api + path,
            {
                withCredentials: true,
                params: options.params
            }
        );
    }

    post<T, R = T>(path: string, body?: T, options: {
        params?: queryParams,
        error_message?: string,
        call_without_token?: boolean,
        force?: boolean
    } = {}): Observable<R> {
        return this._http.post<R>(
            this.paramsService.url_api + path,
            body,
            {
                withCredentials: true,
                params: options.params
            }
        );
    }

    patch<T, R = T>(path: string, body: T, options: {
        params?: queryParams,
        error_message?: string,
        call_without_token?: boolean,
        force?: boolean
    } = {}): Observable<R> {
        return this._http.patch<R>(
            this.paramsService.url_api + path,
            body,
            {
                withCredentials: true,
                params: options.params
            }
        );
    }

    delete<T, R = T>(path: string, options: {
        params?: queryParams,
        error_message?: string,
        call_without_token?: boolean,
        force?: boolean
    } = {}): Observable<R> {
        return this._http.delete<R>(
            this.paramsService.url_api + path,
            {
                withCredentials: true,
                params: options.params
            }
        );
    }
}
