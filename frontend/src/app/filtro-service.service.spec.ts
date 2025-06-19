import { TestBed } from '@angular/core/testing';

import { FiltroServiceService } from './filtro-service.service';

describe('FiltroServiceService', () => {
  let service: FiltroServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FiltroServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
