import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MilkSupply } from './milk-supply';

describe('MilkSupply', () => {
  let component: MilkSupply;
  let fixture: ComponentFixture<MilkSupply>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MilkSupply]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MilkSupply);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
