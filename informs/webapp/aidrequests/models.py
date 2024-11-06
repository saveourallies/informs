from django.db import models


class RegionResponse(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=4, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class AidRequest(models.Model):
    # scope to a region response object
    region_response = models.ForeignKey(RegionResponse, on_delete=models.CASCADE, null=True)
    # 1. Requestor details
    requestor_first_name = models.CharField(max_length=20)
    requestor_last_name = models.CharField(max_length=30)

    requestor_email = models.EmailField()
    requestor_phone = models.CharField(max_length=12)  # Format: 555-555-5555

    # 2. Contact details for party needing assistance
    assistance_first_name = models.CharField(max_length=20, blank=True)
    assistance_last_name = models.CharField(max_length=30, blank=True)
    assistance_email = models.EmailField(blank=True)
    assistance_phone = models.CharField(max_length=12, blank=True)

    # 3. Location of assistance request
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)  # Use two-letter state abbreviations
    zip_code = models.CharField(max_length=5)

    # 4. Type of assistance requested
    ASSISTANCE_CHOICES = [
        ('evacuation', 'Evacuation'),
        ('re_supply', 'Re-supply'),
        ('welfare_check', 'Welfare check'),
        ('other', 'Other (please describe)'),
    ]
    assistance_type = models.CharField(max_length=20, choices=ASSISTANCE_CHOICES)
    assistance_description = models.TextField(blank=True, null=True)

    # 5. Group size
    group_size = models.IntegerField(blank=True, null=True)

    # 6. Preferred contact methods
    contact_methods = models.TextField(blank=True, null=True)

    # 7. Emergency medical needs
    medical_needs = models.TextField(blank=True, null=True)

    # 8. Supplies needed
    supplies_needed = models.TextField(blank=True, null=True)

    # 9. Welfare check information
    welfare_check_info = models.TextField(blank=True, null=True)

    # 10. Additional information
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"AidRequest by {self.requestor_first_name} {self.requestor_last_name} - {self.assistance_type}"
