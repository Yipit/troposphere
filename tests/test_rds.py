import unittest
import troposphere.rds as rds


class TestRDS(unittest.TestCase):

    def test_it_allows_an_rds_instance_created_from_a_snapshot(self):
        rds_instance = rds.DBInstance(
            'SomeTitle',
            AllocatedStorage=1,
            DBInstanceClass='db.m1.small',
            Engine='MySQL',
            DBSnapshotIdentifier='SomeSnapshotIdentifier'
        )

        rds_instance.JSONrepr()

    def test_it_allows_an_rds_instance_with_master_username_and_password(self):
        rds_instance = rds.DBInstance(
            'SomeTitle',
            AllocatedStorage=1,
            DBInstanceClass='db.m1.small',
            Engine='MySQL',
            MasterUsername='SomeUsername',
            MasterUserPassword='SomePassword'
        )

        rds_instance.JSONrepr()

    def test_it_rds_instances_require_either_a_snapshot_or_credentials(self):
        rds_instance = rds.DBInstance(
            'SomeTitle',
            AllocatedStorage=1,
            DBInstanceClass='db.m1.small',
            Engine='MySQL'
        )

        with self.assertRaisesRegexp(
                ValueError,
                'Either \(MasterUsername and MasterUserPassword\) or'
                ' DBSnapshotIdentifier are required'
                ):
            rds_instance.JSONrepr()

    def test_it_allows_an_rds_replica(self):
        rds_instance = rds.DBInstance(
            'SomeTitle',
            AllocatedStorage=1,
            DBInstanceClass='db.m1.small',
            Engine='MySQL',
            SourceDBInstanceIdentifier='SomeSourceDBInstanceIdentifier'
        )

        rds_instance.JSONrepr()

    def test_replica_settings_are_inherited(self):
        rds_instance = rds.DBInstance(
            'SomeTitle',
            AllocatedStorage=1,
            DBInstanceClass='db.m1.small',
            Engine='MySQL',
            SourceDBInstanceIdentifier='SomeSourceDBInstanceIdentifier',
            BackupRetentionPeriod="1",
            DBName="SomeName",
            MasterUsername="SomeUsername",
            MasterUserPassword="SomePassword",
            PreferredBackupWindow="SomeBackupWindow",
            MultiAZ=True,
            DBSnapshotIdentifier="SomeDBSnapshotIdentifier",
            DBSubnetGroupName="SomeDBSubnetGroupName",
        )

        with self.assertRaisesRegexp(
                ValueError,
                'BackupRetentionPeriod, DBName, DBSnapshotIdentifier, '
                'DBSubnetGroupName, MasterUserPassword, MasterUsername, '
                'MultiAZ, PreferredBackupWindow '
                'properties can\'t be provided when '
                'SourceDBInstanceIdentifier is present '
                'AWS::RDS::DBInstance.'
                ):
            rds_instance.JSONrepr()

    def test_it_rds_instances_require_encryption_if_kms_key_provided(self):
        rds_instance = rds.DBInstance(
            'SomeTitle',
            AllocatedStorage=1,
            DBInstanceClass='db.m1.small',
            Engine='MySQL',
            MasterUsername='SomeUsername',
            MasterUserPassword='SomePassword',
            KmsKeyId='arn:aws:kms:us-east-1:123456789012:key/'
                     '12345678-1234-1234-1234-123456789012'
        )

        with self.assertRaisesRegexp(
                ValueError,
                'If KmsKeyId is provided, StorageEncrypted is required'
                ):
            rds_instance.JSONrepr()

    def test_it_allows_an_rds_instance_with_iops(self):
        # ensure troposphere works with longs and ints
        long_number = 2 ** 100
        rds_instance = rds.DBInstance(
            'SomeTitle',
            AllocatedStorage=1,
            DBInstanceClass='db.m1.small',
            Engine='MySQL',
            MasterUsername='SomeUsername',
            MasterUserPassword='SomePassword',
            StorageType='io1',
            Iops=long_number,
        )

        rds_instance.JSONrepr()

    def test_optiongroup(self):
        rds_optiongroup = rds.OptionGroup(
            "OracleOptionGroup",
            EngineName="oracle-ee",
            MajorEngineVersion="12.1",
            OptionGroupDescription="A test option group",
            OptionConfigurations=[
                rds.OptionConfiguration(
                    DBSecurityGroupMemberships=["default"],
                    OptionName="OEM",
                    Port="5500",
                ),
                rds.OptionConfiguration(
                    OptionName="APEX",
                ),
            ]
        )
        rds_optiongroup.JSONrepr()
